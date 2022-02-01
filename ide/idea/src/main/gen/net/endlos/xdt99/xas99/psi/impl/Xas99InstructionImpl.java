// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99.psi.Xas99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99.psi.*;

public class Xas99InstructionImpl extends ASTWrapperPsiElement implements Xas99Instruction {

  public Xas99InstructionImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99Visitor visitor) {
    visitor.visitInstruction(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99Visitor) accept((Xas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xas99ArgsI getArgsI() {
    return findChildByClass(Xas99ArgsI.class);
  }

  @Override
  @Nullable
  public Xas99ArgsII getArgsII() {
    return findChildByClass(Xas99ArgsII.class);
  }

  @Override
  @Nullable
  public Xas99ArgsIII getArgsIII() {
    return findChildByClass(Xas99ArgsIII.class);
  }

  @Override
  @Nullable
  public Xas99ArgsIV getArgsIV() {
    return findChildByClass(Xas99ArgsIV.class);
  }

  @Override
  @Nullable
  public Xas99ArgsIX getArgsIX() {
    return findChildByClass(Xas99ArgsIX.class);
  }

  @Override
  @Nullable
  public Xas99ArgsIXX getArgsIXX() {
    return findChildByClass(Xas99ArgsIXX.class);
  }

  @Override
  @Nullable
  public Xas99ArgsV getArgsV() {
    return findChildByClass(Xas99ArgsV.class);
  }

  @Override
  @Nullable
  public Xas99ArgsVI getArgsVI() {
    return findChildByClass(Xas99ArgsVI.class);
  }

  @Override
  @Nullable
  public Xas99ArgsVIII getArgsVIII() {
    return findChildByClass(Xas99ArgsVIII.class);
  }

  @Override
  @Nullable
  public Xas99ArgsVIIII getArgsVIIII() {
    return findChildByClass(Xas99ArgsVIIII.class);
  }

  @Override
  @Nullable
  public Xas99ArgsVIIIR getArgsVIIIR() {
    return findChildByClass(Xas99ArgsVIIIR.class);
  }

  @Override
  @Nullable
  public Xas99ArgsAdvI getArgsAdvI() {
    return findChildByClass(Xas99ArgsAdvI.class);
  }

  @Override
  @Nullable
  public Xas99ArgsAdvIV getArgsAdvIV() {
    return findChildByClass(Xas99ArgsAdvIV.class);
  }

  @Override
  @Nullable
  public Xas99ArgsAdvIa getArgsAdvIa() {
    return findChildByClass(Xas99ArgsAdvIa.class);
  }

  @Override
  @Nullable
  public Xas99ArgsAdvVI getArgsAdvVI() {
    return findChildByClass(Xas99ArgsAdvVI.class);
  }

  @Override
  @Nullable
  public Xas99ArgsAdvVIII getArgsAdvVIII() {
    return findChildByClass(Xas99ArgsAdvVIII.class);
  }

}
